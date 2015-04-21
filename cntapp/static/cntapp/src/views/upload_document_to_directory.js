define([
        'jquery',
        'views/form',
        'text!templates/documents_upload.html'
    ],
    function ($,
              FormView,
              documentsUploadTemplate) {

        var UploadDocumentToDirectoryView = FormView.extend({

            initialize: function (options) {
                if (!options.parentId) {
                    console.error("no parent id specified");
                    return;
                }
                this.parentId = options.parentId;
                this.template = _.template(documentsUploadTemplate);
            },

            submit: function (event) {
                FormView.prototype.submit.apply(this, arguments);

                var file, data;
                file = $(':file')[0].files[0];
                if (!file) {
                    alert('no file found!');
                    return;
                }

                data = new FormData();
                data.append('name', file.name);
                data.append('file', file);

                console.log('upload file');
                var that = this;
                $.ajax({
                    type: "POST",
                    url: "/api/documents/",
                    data: data,
                    contentType: false,
                    processData: false,
                    success: function (data) {
                        that.done();
                        that.postToDirectory(data.id);
                    },
                    error: function (request, status, error) {
                        alert(request.responseText);
                    }
                });

            },

            postToDirectory: function (documentId) {
                var that = this;
                var url = "/api/directories/" + this.parentId + '/documents/';
                var data = {"documents": documentId};

                $.ajax({
                    type: "POST",
                    traditional: true,
                    url: url,
                    data: data,
                    success: function () {
                        window.history.back();
                    },
                    error: function (request, status, error) {
                        alert(request.responseText);
                    }
                });
            }

        });

        return UploadDocumentToDirectoryView;
    }
);
