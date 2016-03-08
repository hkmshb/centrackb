'use strict';

var appDirectives = angular.module('centrakDirectives', []);

appDirectives.directive('changeOnBlur', function() {
	return {
		restrict: 'A',
		require: 'ngModel',
		link: function(scope, elem, attrs, ngModelCtrl) {
			if (attrs.type === 'radio' || attrs.type === 'checkbox')
				return;
			var callback = attrs.changeOnBlur
			  , oldValue = null
			  , newValue = null;
			
			elem.bind('focus', function() {
				scope.$apply(function() {
					oldValue = elem.val();
				});
			});
			elem.bind('blur', function() {
				scope.$apply(function() {
					var newValue = elem.val();
					if (newValue !== oldValue) {
						scope.oldValue = oldValue;
						scope.newValue = newValue;
						scope.$eval(callback);
					}
				})
			});
		}
	};
});