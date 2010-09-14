// Non-UI filter code, for use in multiple applications.

// Global declaration for JSLint (http://www.jslint.com/)
/*global console, dojo, dojox, gobotany */

dojo.provide('gobotany.filters');
dojo.require('dojox.data.JsonRestStore');

// Filter
//
// Base for the different types of filters.
//
dojo.declare("gobotany.filters.Filter", null, {
    character_short_name: "",
    friendly_name: "",
    order: 0,
    pile_slug: "",
    value_type: "",
    unit: "",
    key_characteristics: null,
    notable_exceptions: null,
    selected_value: null,
    filter_callback: null,
    constructor: function(args) {
        this.character_short_name = args.character_short_name;
        this.friendly_name = args.friendly_name;
        this.order = args.order;
        this.pile_slug = args.pile_slug;
        this.value_type = args.value_type;
        this.unit = args.unit;
        this.filter_callback = args.filter_callback;
        dojo.safeMixin(this, args);
        var url = '/piles/' + this.pile_slug + '/' + 
                  this.character_short_name + '/';
        this.store = new dojox.data.JsonRestStore({target: url});
    },
    load_values: function(args) {
        if (args && args.onLoaded) {
            args.onLoaded();
        }
    }
});


// MultipleChoiceFilter
//
dojo.declare("gobotany.filters.MultipleChoiceFilter", 
             [gobotany.filters.Filter], {
    values: null,
    constructor: function(args) {
        this.values = [];
    },
    load_values: function(args) {
        this.store.fetch({
            scope: this,
            onComplete: function(response) {
                dojo.forEach(response, this.process_value, this);
                if (args && args.onLoaded) {
                    args.onLoaded();
                }
            }
        });
    },
    process_value: function(character_value, index) {
        this.values.push(character_value);
    }
});


// NumericRangeFilter
//
dojo.declare('gobotany.filters.NumericRangeFilter',
             [gobotany.filters.MultipleChoiceFilter], {
    process_value: function(character_value, index) {
        // We make this.values an object: {min: a, max: b}
        if (this.values.length == 0) this.values = {};
        if (character_value.value == null) return;
        var v = this.values;
        var vmin = character_value.value[0];
        var vmax = character_value.value[1];
        if (vmin != null && (v.min == null || v.min > vmin)) v.min = vmin;
        if (vmax != null && (v.max == null || v.max < vmax)) v.max = vmax;
    }
});


// FilterManager
//
// A FilterManager object is responsible for pulling a pile's filters from
// the REST API and maintaining a collection.
// It pulls a set of default filters, then later would pull more filters
// as needed.
//
dojo.declare("gobotany.filters.FilterManager", null, {
    pile_slug: "",
    character_groups: null,
    filters: null,
    species_count: 0,
    species_ids: [],
    entries: [],
    constructor: function(args) {
        this.pile_slug = args.pile_slug;
        this.character_groups = [];
        this.plant_preview_characters = [];
        this.filters = [];
        this.filters_loading = 0;

        if (!args.pile_url) args.pile_url = '/piles/';
        if (!args.taxon_url) args.taxon_url = '/taxon/';
        this.store = new dojox.data.JsonRestStore({target: args.pile_url});
        this.chars_store = new dojox.data.JsonRestStore({target: args.pile_url + args.pile_slug + '/characters/'});
        this.result_store = new dojox.data.JsonRestStore({target: args.taxon_url, 
                                                          idAttribute: 'scientific_name'});
    },

    query_best_filters: function(args) {
        var choose_best = 3;
        if (args.choose_best)
            choose_best = args.choose_best;
        this.chars_store.fetch({
            query: {choose_best: choose_best,
                    species_id: this.species_ids || [],
                    character_group_id: args.character_group_ids || [],
                    exclude: args.existing_characters || [],
                    include_filter: 1},
            scope: {filter_manager: this, args: args},
            onComplete: this._load_incoming_filters,
        });
    },
    query_filters: function(args) {
        this.chars_store.fetch({
            query: {include: args.short_names || [], include_filter: 1},
            scope: {filter_manager: this, args: args},
            onComplete: this._load_incoming_filters,
        });
    },
    _load_incoming_filters: function(items) {
        var lst = [];
        for (var x = 0; x < items.length; x++) {
            var item = items[x];
            lst.push(this.filter_manager.add_filter({
                filter_json: {
                    character_friendly_name: item.friendly_name,
                    character_short_name: item.short_name,
                    order: 0,
                    notable_exceptions: item.filter.notable_exceptions,
                    key_characteristics: item.filter.key_characteristics,
                    value_type: item.value_type,
                    unit: item.unit,
                    pile_slug: this.filter_manager.pile_slug
                },
            }));
        }
        this.args.onLoaded(lst);
    },

    load_pile_info: function(args) {
        var store = this.store;
        store.fetchItemByIdentity({
            scope: {args: args, filter_manager: this},
            identity: this.pile_slug,
            onItem: function(item) {
                // Save the character groups for this pile.
                this.filter_manager.character_groups = item.character_groups;
                
                // Save the plant preview characters for this pile.
                this.filter_manager.plant_preview_characters =
                    item.plant_preview_characters;
                this.filter_manager.on_character_groups_changed();

                if (args && args.load_default_filters) {
                    // Start off with the default filters for this pile.
                    this.filter_manager.filters_loading =
                        item.default_filters.length;
                    for (var y = 0; y < item.default_filters.length; y++) {
                        var filter_json = item.default_filters[y];
                        this.filter_manager.add_filter({
                            filter_json: filter_json,
                            onAdded: dojo.hitch(this, 
                                this.filter_manager._watch_default_filters_loading)
                        });
                    }
                } else {
                    this.filter_manager.on_pile_info_loaded();
                }
            }
        });
    },
    _watch_default_filters_loading: function(data) {
        // scope should be an object with filter_manager and onLoaded attrs

        this.filter_manager.filters_loading--;
        if (this.filter_manager.filters_loading === 0) {
            if (this.args && this.args.onLoaded)
                this.args.onLoaded();
            this.filter_manager.on_pile_info_loaded();
            this.filter_manager.on_default_filters_loaded();
        }
    },
    on_pile_info_loaded: function() {},
    on_character_groups_changed: function() {},
    on_default_filters_loaded: function() {},

    build_filter: function(args) {
        var filter_json = args.filter_json;
        var filter_type;

        if (filter_json.value_type == 'LENGTH') {
            filter_type = gobotany.filters.NumericRangeFilter;
        }
        else if (filter_json.value_type == 'TEXT')  {
            filter_type = gobotany.filters.MultipleChoiceFilter;
        }
        else {
            filter_type = gobotany.filters.Filter;
        }

        var filter = new filter_type(
            {
                friendly_name: filter_json.character_friendly_name,
                character_short_name: filter_json.character_short_name,
                order: filter_json.order,
                notable_exceptions: filter_json.notable_exceptions,
                key_characteristics: filter_json.key_characteristics,
                value_type: filter_json.value_type,
                unit: filter_json.unit,
                pile_slug: this.pile_slug
            }
        );

        if (args && args.onAdded) {
            filter.load_values({onLoaded: dojo.hitch(this, function() {
                args.onAdded(filter);
            })});
        } else {
            filter.load_values({});
        }
        
        return filter;
    },
    has_filter: function(short_name) {
        for (var x = 0; x < this.filters.length; x++)
            if (this.filters[x].character_short_name == short_name)
                return true;
        return false;
    },
    remove_filter: function(short_name) {
        for (var x = 0; x < this.filters.length; x++) {
            if (this.filters[x].character_short_name == short_name) {
                var filter = this.filters[x];
                this.filters.splice(x, 1);
                this.on_filter_removed(filter);
                return;
            }
        }
    },
    add_filter: function(args) {
        // Add the filter to the manager's collection of filters.
        var f = this.build_filter(args);
        this.filters.push(f);
        console.log('add_filter: '+f.character_short_name);
        this.on_filter_added(f);
        return f;
    },
    add_special_filter: function(args) {
        var filter = new gobotany.filters.Filter({
            friendly_name: '', // not needed yet
            character_short_name: args.character_short_name,
            order: 0,
            notable_exceptions: null,
            key_characteristics: null,
            value_type: null,
            unit: null,
            pile_slug: this.pile_slug,
            filter_callback: args.filter_callback
        });
        this.filters.push(filter);
        console.log('add_special_filter: '+filter.character_short_name);
        this.on_filter_added(filter);
    },
    set_selected_value: function(character_short_name, selected_value) {
        for (var i = 0; i < this.filters.length; i++) {
            if (this.filters[i].character_short_name === 
                  character_short_name) {
                // Character values must be stringified, since their
                // .length is checked before allowing them to become
                // part of our query URL.
                if (selected_value != null)
                    selected_value = String(selected_value);
                this.filters[i].selected_value = selected_value;
                this.on_filter_changed(this.filters[i], selected_value);
                return;
            }
        }
        console.log('FilterManager cannot set a value for unknown filter',
                    character_short_name)
    },
    get_selected_value: function(character_short_name) {
        var selected_value = null;
        var found_filter = false;
        var i = 0;
        while (!found_filter && i < this.filters.length) {
            if (this.filters[i].character_short_name === 
                character_short_name) {

                var value = this.filters[i].selected_value;
                if (value !== null && value.length) {
                    selected_value = value;
                }
                found_filter = true;
            }
            i++;
        }
        return selected_value;
    },
    on_filter_added: function(filter) {},
    on_filter_removed: function(filter) {},
    on_filter_changed: function(filter) {},

    as_query_string: function() {
        var filter_names = [];
        var obj = {};
        for (var x = 0; x < this.filters.length; x++) {
            var f = this.filters[x];
            filter_names.push(f.character_short_name);
            obj[f.character_short_name] = f.selected_value;
        }

        return '_filters='+filter_names.join(',')+'&'+dojo.objectToQuery(obj);
    },

    empty_filters: function() {
        this.filters = [];
    },
    run_filtered_query: function(onComplete) {
        var content = {pile: this.pile_slug};
        var special = [];
        console.log('FilterManager: running filtered query');
        for (var i = 0; i < this.filters.length; i++) {
            var filter = this.filters[i];
            if (filter.filter_callback != null) {
                special.push(filter);
            } else if (filter.selected_value !== null && 
                     filter.selected_value.length) {

                content[filter.character_short_name] = filter.selected_value;
            }
        }

        this.result_store.fetch({
            scope: this,
            query: content,
            onComplete: function(data) {
                this.species_count = data.items.length;
                this.species_ids = [];
                for (i=0; i < data.items.length; i++)
                    this.species_ids[i] = data.items[i].id;

                if (special.length > 0) {
                    // run special filters
                    var newdata = [];
                    for (var x = 0; x < data.items.length; x++) { 
                        var item = data.items[x];
                        var removed = false;
                        for (var y = 0; y < special.length; y++) {
                            var callback = special[y].filter_callback;
                            if (!callback(special[y], item)) {
                                removed = true;
                                break;
                            }
                        }

                        if (!removed)
                            newdata.push(item);
                    }
                    data.items = newdata;
                    console.log('FilterManager.run_filtered_query: data was specially filtered');
                }

                // Call the passed-in callback function.
                onComplete(data);
            },
            onError: function(error) {
                console.log('Taxon search encountered an error!');
                console.log(error);
            }
        });
    }
});
