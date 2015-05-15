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
                maxFilesize: 1024,  // MB
                maxThumbnailFilesize: 5,  // MB
                acceptedFiles: "image/*,audio/*,video/*,application/pdf,.apk",

                init: function () {
                    this.on('addedfile', function (file) {
                        console.log(file);
                    });
                    this.on("sending", function (file, xhr, formData) {
                        // TODO: change file name here
                        formData.append("name", file.name);
                    });
                    this.on('processing', function (file) {
                        console.log('processing:' + file.name);
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
