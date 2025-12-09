/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { Component, useState, onMounted} from "@odoo/owl";


class AIAgentSystray extends Component {
    setup() {
        this.state = useState({
            messages: [],
            inputMessage: "",
            isOpen: false,
            isLoading: false,
            conversationHistory: [],
        });
        onMounted(() => {
            if (this.state.isOpen) {
                this.scrollToBottom();
            }
        });
    }
    
    async sendMessage() {
        if (!this.state.inputMessage.trim() || this.state.isLoading) return;

        const message = this.state.inputMessage;
        this.state.messages.push({ content: message, isUser: true, isHtml: false });
        this.state.inputMessage = "";
        this.state.isLoading = true;

        try {
            // Get configuration from Odoo system parameters with fallback to defaults
            let config;
            try {
                config = await rpc("/ai_agent/config");
            } catch (rpcError) {
                console.warn("Failed to fetch config from server, using defaults:", rpcError);
                // Fallback to default configuration
                config = {
                    service_url: 'https://openrouter.ai/api/v1/chat/completions',
                    api_key: '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'
                };
            }
            
            // Prepare conversation history
            const conversationHistory = this.state.conversationHistory.map(msg => ({
                role: msg.isUser ? "user" : "assistant",
                content: msg.content
            }));

            // Add current message to history
            conversationHistory.push({
                role: "user",
                content: message
            });

            // Enhance the prompt with relevant Odoo data if needed
            const enhancedConversation = await this.enhanceWithOdooData(conversationHistory);

            // Make the call to OpenRouter API with retry logic for rate limiting
            let retries = 3;
            let delay = 1000;
            
            while (retries >= 0) {
                try {
                    const response = await fetch(config.service_url, {
                        method: "POST",
                        headers: { 
                            "Content-Type": "application/json", 
                            "Authorization": "Bearer " + config.api_key,
                            "HTTP-Referer": window.location.origin,
                            "X-Title": "Odoo AI Assistant"
                        },
                        body: JSON.stringify({
                            "model": "nousresearch/hermes-3-llama-3.1-405b:free",
                            "messages": enhancedConversation
                        }),
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        console.error("API error details:", errorData);
                        
                        // If it's a rate limit error and we have retries left, wait and retry
                        if (response.status === 429 && retries > 0) {
                            // Show a message to the user that we're retrying
                            const retryMessage = `Rate limited. Retrying in ${delay}ms... (${retries} attempts left)`;
                            // Update the last message or add a new one
                            if (this.state.messages.length > 0 && this.state.messages[this.state.messages.length - 1].isUser === false) {
                                // Update the last AI message
                                this.state.messages[this.state.messages.length - 1].content = retryMessage;
                            } else {
                                // Add a new message
                                this.state.messages.push({ content: retryMessage, isUser: false, isHtml: false });
                            }
                            
                            console.log(retryMessage);
                            await new Promise(resolve => setTimeout(resolve, delay));
                            delay *= 2; // Exponential backoff
                            retries--;
                            continue;
                        }
                        
                        throw new Error(JSON.stringify(errorData));
                    }

                    const data = await response.json();

                    // Render AI response as HTML (sanitize only, since LLM returns HTML)
                    const content = data.choices[0].message.content;
                    const html = window.DOMPurify.sanitize(content);
                    this.state.messages.push({ content: html, isUser: false, isHtml: true });
                    this.state.conversationHistory = enhancedConversation.concat([{
                        role: "assistant",
                        content: content
                    }]);

                    // Scroll to bottom of chat after DOM update
                    setTimeout(() => this.scrollToBottom(), 0);
                    return; // Success, exit the retry loop
                    
                } catch (error) {
                    if (retries > 0) {
                        const retryMessage = `Request failed. Retrying in ${delay}ms... (${retries} attempts left)`;
                        // Update the last message or add a new one
                        if (this.state.messages.length > 0 && this.state.messages[this.state.messages.length - 1].isUser === false) {
                            // Update the last AI message
                            this.state.messages[this.state.messages.length - 1].content = retryMessage;
                        } else {
                            // Add a new message
                            this.state.messages.push({ content: retryMessage, isUser: false, isHtml: false });
                        }
                        
                        console.log(retryMessage);
                        await new Promise(resolve => setTimeout(resolve, delay));
                        delay *= 2; // Exponential backoff
                        retries--;
                        continue;
                    }
                    throw error; // No more retries, rethrow the error
                }
            }
        } catch (error) {
            let errorMessage = "Error: " + error.message;
            
            // Provide user-friendly error messages
            if (error.message.includes("429")) {
                errorMessage = "Rate limit exceeded. Please try again in a few minutes or consider using your own API key for better performance. You can get your own key at https://openrouter.ai/settings/integrations";
            } else if (error.message.includes("Unauthorized") || error.message.includes("401")) {
                errorMessage = "API authentication failed. Please check your API key configuration.";
            } else if (error.message.includes("NetworkError")) {
                errorMessage = "Network connection error. Please check your internet connection.";
            } else if (error.message.includes("Connection to") && error.message.includes("couldn't be established")) {
                errorMessage = "Could not connect to the AI service. Please check your configuration and network connection.";
            }
            
            this.state.messages.push({ content: errorMessage, isUser: false, isHtml: false });
            console.error("Error:", error);
        } finally {
            this.state.isLoading = false;
        }
    }

    handleKeyPress(ev) {
        if (ev.key === "Enter" && !ev.shiftKey) {
            ev.preventDefault();
            this.sendMessage();
        }
    }

    scrollToBottom() {
        if (!this.el) return;
        const chatContainer = this.el.querySelector(".o_chat_container");
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }

    async enhanceWithOdooData(conversationHistory) {
        // Check if the conversation contains queries about partners, products, or sale orders
        const lastUserMessage = conversationHistory[conversationHistory.length - 1];
        
        if (!lastUserMessage || lastUserMessage.role !== 'user') {
            return conversationHistory;
        }
        
        const messageContent = lastUserMessage.content.toLowerCase();
        
        // Enhanced conversation with context
        const enhancedConversation = [...conversationHistory];
        
        // Add context about available data access capabilities
        const contextMessage = {
            role: "system",
            content: "You are an Odoo AI assistant with access to company data. You can access partners, products, and sale orders data through specific API endpoints. " +
                    "When asked about specific business data, you should formulate appropriate queries to retrieve that data. " +
                    "The available endpoints are: /ai_agent/data/partners, /ai_agent/data/products, and /ai_agent/data/sale_orders. " +
                    "Always provide accurate and helpful responses based on the actual data."
        };
        
        // Insert context at the beginning
        enhancedConversation.unshift(contextMessage);
        
        return enhancedConversation;
    }

    toggleChat() {
        this.state.isOpen = !this.state.isOpen;
        if (this.state.isOpen) {
            // Use setTimeout to ensure the DOM is updated before scrolling
            setTimeout(() => this.scrollToBottom(), 0);
        }
    }
}

AIAgentSystray.template = "ai_agent_odoo.AIAgentSystray";
AIAgentSystray.props = {};
AIAgentSystray.components = {};

// Add the widget to the systray
registry.category("systray").add("ai_agent_odoo.AIAgentSystray", {
    Component: AIAgentSystray,
});