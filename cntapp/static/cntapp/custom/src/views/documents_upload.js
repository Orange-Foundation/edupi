define([
        'jquery',
        'views/form',
        'text!templates/documents_upload.html'
    ],
    function ($,
              FormView,
              documentsUploadTemplate) {

        var DocumentsUploadView = FormView.extend({

            initialize: function () {
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

                var that = this;
                $.ajax({
                    type: "POST",
                    url: "/api/documents/",
                    data: data,
                    contentType: false,
                    processData: false,
                    success: function (data) {
                        that.done();
                        window.location.replace("/api/documents/" + data.id + '/');
                    },
                    error: function (request, status, error) {
                        alert(request.responseText);
                    }
                });

            }
        });

        return DocumentsUploadView;
    }
);