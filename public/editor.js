/**
 * Created by prism on 5/30/14.
 */
$(function() {
    $('.raptor-editable').raptor({
        plugins: {
            // Define which save plugin to use. May be saveJson or saveRest
            save: {
                plugin: 'saveJson'
            },
            // Provide options for the saveJson plugin
            saveJson: {
                // The URL to which Raptor data will be POSTed
                url: 'http://localhost:8000/users/editor',
                // The parameter name for the posted data
                postName: 'raptor-content',
                // A string or function that returns the identifier for the Raptor instance being saved
                id: function() {
                    return this.raptor.getElement().data('id');
                }
            }
        }
    });
});