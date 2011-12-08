require([
    'activate_search_suggest',
    'shadowbox',
    'shadowbox_close'
]);

require([
    'dojo_config',
    '/static/js/dojo/dojo.js',
    '/static/js/layers/sk.js',
    'sidebar',
    'simplekey/resources'
], function() {

    dojo.require('gobotany.sk.species');
    dojo.addOnLoad(function() {
        var helper = gobotany.sk.species.SpeciesPageHelper();
        helper.setup();
    });    

});

require([
    'activate_smooth_div_scroll'
]);
