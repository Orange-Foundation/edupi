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
                return kBytes + (si ? i18n.t('KB') : i18n.t(' KiB'));
            }
            var units = si
                ? ['MB','GB','TB','PB','EB','ZB','YB']
                : ['MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];

            // localization
            var i, length = units.length;
            for (i = 0; i < length; i++) {
                units[i] = i18n.t(units[i])
            }

            var u = -1;
            do {
                kBytes /= thresh;
                ++u;
            } while(Math.abs(kBytes) >= thresh && u < units.length - 1);

            return Number(kBytes.toFixed(1)).toLocaleString(cntapp.getCookie('i18next') || 'en') + ' ' +units[u];
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
                        [i18n.t("version"), result["CurrentVersion"]],
                        [i18n.t("used-storage"), that.toHumanReadableSize(cntappInfo["Used"])],
                        [i18n.t("directories"), cntappInfo["TotalDirectories"]],
                        [i18n.t("documents"), cntappInfo["TotalDocuments"]],
                        [i18n.t("document-references"), cntappInfo["TotalDocumentsReferences"]],
                    ];

                    fileSystemInfoTable = [
                        [i18n.t("total-size"), that.toHumanReadableSize(fileSystemInfo["TotalSize"])],
                        [i18n.t("used"), that.toHumanReadableSize(fileSystemInfo["Used"])
                            + " (" + fileSystemInfo["UsedPercentage"]+ ")"
                        ],
                        [i18n.t("available"), that.toHumanReadableSize(fileSystemInfo["Available"])],
                    ];

                    context = {
                        "cntappInfoTable": cntappInfoTable,
                        "fileSystemInfoTable": fileSystemInfoTable
                    };

                    that.$el.html(that.template(context));
                    that.$el.i18n();
                });
            return this;
        }
    });

    return SysInfoView;
});
