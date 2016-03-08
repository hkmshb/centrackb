'use strict';

var centrakServices = angular.module('centrakServices', []);
centrakServices.factory('Capture', ['$resource',
    function($resource){
        return $resource('api/captures/:captureId/', {}, {
            query: {method:'GET', params:{captureId:''}}
        });
    }
])