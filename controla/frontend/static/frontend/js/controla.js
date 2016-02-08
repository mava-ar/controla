/**
 * Created by matuu on 29/01/16.
 */
(function($) {
    function showConfirm(title, message, callback_yes, callback_no) {
        BootstrapDialog.confirm({
            title: title,
            message: message,
            type: BootstrapDialog.TYPE_DANGER,
            closable: true, // <-- Default value is false
            draggable: true, // <-- Default value is false
            btnCancelLabel: 'No, cancelar!', // <-- Default value is 'Cancel',
            btnOKLabel: 'Si, continuar!', // <-- Default value is 'OK',
            btnOKClass: 'btn-primary',
            callback: function (result) {
                // result will be true if button was click, while it will be false if users close the dialog directly.
                if (result) {
                    try {
                        callback_yes();
                    } catch (e) {
                        console.log(e);
                    }
                } else {
                    try {
                        if (callback_no != undefined)
                            callback_no();
                    } catch (e) {
                        console.log(e);
                    }

                }
            }
        });
    }
})(jQuery);