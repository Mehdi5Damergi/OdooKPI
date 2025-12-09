/* @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { Component, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class CaptureEmployeeImage extends Component {
    static template = "CaptureEmployeeImage";

    setup() {
        // Prevent recursion by checking if already initialized
        if (this._isInitialized) return;
        this._isInitialized = true;
        
        super.setup();
        this.employee_id = this.props.action.params.employee_id || this.props.action.params.active_id;
        this.orm = useService("orm");
        this.action = useService("action");
        try {
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                alert("Unable to access the camera");
                this.env.config.historyBack();
            } else {
                onMounted(async () => {
                    // Prevent multiple executions
                    if (this._isStreamStarted) return;
                    this._isStreamStarted = true;
                    this._start_video_stream();
                    this._bind_events();
                })
            }
        }
        catch (error) {
            console.log(error);
        }
    }

    _start_video_stream() {
        // Prevent multiple streams
        if (this._streamStarted) return;
        this._streamStarted = true;
        
        const self = this;
        setTimeout(() => {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function (stream) {
                    var video = document.getElementById('video');
                    if (video) {
                        video.srcObject = stream;
                    }
                })
                .catch(function (err) {
                    self._stop_stream();
                    alert("Unable to access the camera");
                    self.env.config.historyBack();
                });
        }, 500);
    }

    _bind_events() {
        // Prevent multiple event bindings
        if (this._eventsBound) return;
        this._eventsBound = true;
        
        // Using modern event listeners instead of jQuery
        const closeBtn = document.getElementById('btn-close');
        const clickBtn = document.getElementById('btn-click');
        const closeSubBtn = document.getElementById('btn-close-sub');
        
        if (closeBtn) closeBtn.addEventListener('click', this._on_close.bind(this));
        if (clickBtn) clickBtn.addEventListener('click', this._on_capture.bind(this));
        if (closeSubBtn) closeSubBtn.addEventListener('click', this._on_close.bind(this));
    }

    _on_capture() {
        // Prevent multiple captures
        if (this._isCapturing) return;
        this._isCapturing = true;
        
        try {
            const self = this;

            var video = document.getElementById('video');
            var canvas = document.getElementById('canvas');
            
            if (!video || !canvas) {
                this._isCapturing = false;
                return;
            }
            
            var context = canvas.getContext('2d');

            const targetWidth = 320;
            const targetHeight = 240;

            canvas.width = targetWidth;
            canvas.height = targetHeight;

            context.drawImage(video, 0, 0, targetWidth, targetHeight);

            var imageData = canvas.toDataURL('image/png');

            this.orm.call('hr.employee', 'register_face',[this.employee_id, imageData])
            .then(function (result) {
                self._on_close();
            })
            .catch(function(error) {
                console.error("Error saving image:", error);
                self._on_close();
            })
            .finally(function() {
                self._isCapturing = false;
            });
        } catch (error) {
            console.error("Error during capture:", error);
            this._isCapturing = false;
            this._on_close();
        }
    }

    _stop_stream() {
        var video = document.getElementById('video');
        if (video && video.srcObject) {
            let tracks = video.srcObject.getTracks();
            tracks.forEach(track => track.stop());
            video.srcObject = null;
        }
    }

    _on_close() {
        // Prevent multiple closings
        if (this._isClosing) return;
        this._isClosing = true;
        
        this._stop_stream();
        this.env.config.historyBack();
    }
    
}

registry.category("actions").add("new_employee_image", CaptureEmployeeImage);