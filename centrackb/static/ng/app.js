'use strict';

var centrakApp = angular.module('centrakApp', [
    'centrakDirectives',
    'centrakControllers',
]);

centrakApp.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol(':{');
	$interpolateProvider.endSymbol('}:');
});



