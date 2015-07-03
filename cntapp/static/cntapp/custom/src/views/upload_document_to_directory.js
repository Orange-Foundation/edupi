define([
        'jquery',
        'dropzone',
        'views/form',
        'text!templates/upload.html'
    ],
    function ($,
              Dropzone,
              FormView,
              uploadTemplate) {

        var UploadView, initDropzone;

        initDropzone = function (view) {
            view.$('#file-dropzone').dropzone({
                url: '/api/documents/',
                paramName: "file",
                maxFilesize: 200,  // MB
                maxThumbnailFilesize: 5,  // MB
                parallelUploads: 1,
                acceptedFiles: "image/*,audio/*,video/*,application/pdf,.apk," +
                    // office files
                ".ppt,.pptx,.pot,.potx,.pps,.ppsx,.ppa," +
                ".doc,.docx,.dot,.dotx," +
                ".xls,.xlsx,.xlt,.xltx,.xla",

                init: function () {
                    var uploadInfo = function (msg) {
                        this.$('.upload-info').html(msg)
                    };

                    this.on('addedfile', function (file) {
                        console.log(file);
                    });
                    this.on("sending", function (file, xhr, formData) {
                        formData.append("name", file.name);
                        formData.append("csrfmiddlewaretoken", cntapp.csrfToken);
                    });
                    this.on('processing', function (file) {
                        view.$('.btn-finish').attr('disabled', true);
                        uploadInfo('Uploading: ' + file.name);
                    });
                    this.on("uploadprogress", function (file, progress, bytesSent) {
                        if (progress === 100) {
                            // the server need times to copy the file, and generate thumbnail.
                            uploadInfo('Processing:' + file.name);
                        }
                    });
                    this.on('queuecomplete', function (uploadProgress, totalBytes, totalBytesSent) {
                        uploadInfo('Upload complete!');
                        view.$('.btn-finish').attr('disabled', false);
                    });
                    this.on('success', function (file, json) {
                        console.log(json);
                        var url = "/api/directories/" + view.parentId + '/documents/';
                        var data = {"documents": json['id']};
                        $.ajax({
                            type: "POST",
                            traditional: true,
                            url: url,
                            data: data,
                            error: function (request, status, error) {
                                alert(error);
                            }
                        });
                    });
                }  // end of init
            });
        };

        UploadView = Backbone.View.extend({
            initialize: function (options) {
                this.parentId = options.parentId;
                this.path = options.path;
                this.template = _.template(uploadTemplate)
            },

            render: function () {
                this.$el.html(this.template());
                this.$el.i18n();
                initDropzone(this);
                return this;
            },

            events: {
                'click .btn-finish': function () {
                    cntapp.router.navigate('#directories/' + this.path, {trigger: true});
                }
            }
        });

        return UploadView;
    }
);
