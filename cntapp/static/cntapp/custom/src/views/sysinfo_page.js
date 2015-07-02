define([
    'underscore',
    'backbone',
    'text!templates/sys_info_page.html'
], function (_, Backbone, sysInfoPageTemplate) {
    var SysInfoView = Backbone.View.extend({

        initialize: function (options) {
            this.template = _.template(sysInfoPageTemplate);
        },

        toHumanReadableSize: function (kBytes, si) {
            // credit: http://stackoverflow.com/questions/10420352/converting-file-size-in-bytes-to-human-readable
            var thresh = si ? 1000 : 1024;
            if(Math.abs(kBytes) < thresh) {
                return kBytes + (si ? 'KB' : ' KiB');
            }
            var units = si
                ? ['MB','GB','TB','PB','EB','ZB','YB']
                : ['MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];
            var u = -1;
            do {
                kBytes /= thresh;
                ++u;
            } while(Math.abs(kBytes) >= thresh && u < units.length - 1);
            return kBytes.toFixed(1)+' '+units[u];
        },

        render: function () {
            var that = this;
            //this.$el.html('please wait...');
            $.get('/custom/sys_info/')
                .done(function (result) {
                    var cntappInfo, cntappInfoTable,
                        fileSystemInfo, fileSystemInfoTable,
                        context;

                    cntappInfo = result["cntapp"];
                    fileSystemInfo = result["fileSystem"];

                    cntappInfoTable = [
                        ["Current version", result["CurrentVersion"]],
                        ["Used Storage", that.toHumanReadableSize(cntappInfo["Used"])],
                        ["Directories", cntappInfo["TotalDirectories"]],
                        ["Documents", cntappInfo["TotalDocuments"]],
                        ["Documents' references", cntappInfo["TotalDocumentsReferences"]],
                    ];

                    fileSystemInfoTable = [
                        ["Total size", that.toHumanReadableSize(fileSystemInfo["TotalSize"])],
                        ["Used", that.toHumanReadableSize(fileSystemInfo["Used"])
                            + " (" + fileSystemInfo["UsedPercentage"]+ ")"
                        ],
                        ["Available", that.toHumanReadableSize(fileSystemInfo["Available"])],
                    ];

                    context = {
                        "cntappInfoTable": cntappInfoTable,
                        "fileSystemInfoTable": fileSystemInfoTable
                    };

                    that.$el.html(that.template(context));
                });
            return this;
        }
    });

    return SysInfoView;
});
