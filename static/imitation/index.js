app.directive('imitation', function(Socket){
  return {
    restrict: 'E',
    templateUrl: 'static/imitation/tpl.html',
    scope: {},
    controller: function($scope){
      $scope.files = [];
      $scope.file;
      $scope.columns = [];
      $scope.slectColumns = false;

      Socket.on('csv/data', function(response) {
        $scope.data = response.data;
        $scope.columns = _.map(response.columns, function(name) {
          return {
            active: true,
            name: name
          };
        });

        $scope.$apply();
      });

      $scope.load = function(filename) {
        $scope.file = filename;
        Socket.emit('csv/data', { filename: filename });
      };

      Socket.on('csv/files', function(files) {
        $scope.files = files;
        $scope.file = _.first($scope.files);
        $scope.load($scope.file);
      });

      Socket.emit('csv/files');

      Socket.on('csv/files', function(files) {
        $scope.files = files;
        $scope.$apply();
      });

      Socket.on('csv/imitate', function(samples) {
        console.log(samples);
      });

      function getSelectedColumns() {
        var columns = _.filter($scope.columns, function(column){
          return column.active;
        });
        return _.map(columns, 'name');
      };

      $scope.imitate = function() {
        console.log(getSelectedColumns());
        Socket.emit('csv/imitate', {
          filename: $scope.file,
          columns: getSelectedColumns()
        });
      };
    }
  };
});
