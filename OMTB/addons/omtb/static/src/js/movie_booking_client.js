odoo.define('bookingreservation.movie', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var core = require('web.core');
var rpc = require('web.rpc');
var session = require('web.session');
var web_client = require('web.web_client');
var _t  = core._t;
var QWeb = core.qweb;

var MovieDashboard = AbstractAction.extend({
    template: 'MovieBookingClientAction',

    init: function(parent, context){
        console.log("INIT");
        this._super(parent, context);
        this.dashboards_templates = ['MovieDashboard'];
    },

    willStart: function(){
        var self = this;
        return self.fetch_data();
    },

    start: function(){
        console.log("Start")
        var self = this;
        this.set("title", 'Dashboard');
        return this._super().then(function(){
        });
    },

    fetch_data: function(){
        console.log("Fetch")
        var self = this;

        var def1 = this._rpc({
            model: 'movie.details',
            method : 'get_movies_info',
        }).then(function(result){
               console.log(result)
               self.data = result;
        });


        return $.when(def1);
    },
});
core.action_registry.add('movie_dashboard', MovieDashboard);
return MovieDashboard;
});