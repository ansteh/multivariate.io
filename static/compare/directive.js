app.directive('compare', function(Socket){
  return {
    restrict: 'E',
    templateUrl: 'static/compare/index.tpl.html',
    scope: {
      columns: "="
    },
    controller: function($scope) {
      
    }
  };
});

app.directive('variableCompare', function(Socket) {
  return {
    restrict: 'E',
    templateUrl: 'static/compare/variable-compare.tpl.html',
    scope: {
      column: "="
    },
    controller: function($scope, $element) {
      var chartX = Graphics.scatter($element.find('#compare-x')[0]);
      var chartY = Graphics.scatter($element.find('#compare-y')[0]);

      chartX.plot({
        x_accessor: $scope.column.x_accessor,
        y_accessor: $scope.column.y_accessor,
        data: _.map($scope.column.data, function(item, index) {
          return { x: index, y: _.get(item, $scope.column.x_accessor) }
        })
      });

      chartY.plot({
        x_accessor: $scope.column.x_accessor,
        y_accessor: $scope.column.y_accessor,
        data: _.map($scope.column.data, function(item, index) {
          return { x: index, y: _.get(item, $scope.column.y_accessor) }
        })
      });
    }
  };
});
