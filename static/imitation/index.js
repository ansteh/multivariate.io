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
      $scope.data;
      $scope.realDataLength;
      $scope.simulatedDataLength;

      $scope.plotColumns = {};

      $scope.getActiveColumns = function() {
        return _.filter($scope.columns, 'active');
      };

      $scope.getColumnsForPlot = function() {
        if($scope.columns.length >= 2) {
          var columns = $scope.getActiveColumns();
          return columns;
        }
        return [];
      };

      $scope.updatePlotColumns = function() {
        if($scope.columns.length >= 2) {
          var columns = $scope.getActiveColumns();
          $scope.plotColumns.x = columns[0]['name'];
          $scope.plotColumns.y = columns[1]['name'];
        }
      };

      getNow = function() {
        return Date.now().toString();
      };
      $scope.now = getNow();

      Socket.on('csv/data', function(response) {
        $scope.data = response.data;
        $scope.columns = _.map(response.columns, function(name) {
          return {
            active: true,
            name: name
          };
        });

        $scope.updatePlotColumns();

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

      Socket.on('csv/imitate', function(info) {
        console.log(info);
        $scope.realDataLength = _.get(info, 'real_data_length');
        $scope.simulatedDataLength = info.simulated.length;
        $scope.now = getNow();
        $scope.$apply();
      });

      function getSelectedColumns() {
        var columns = _.filter($scope.columns, function(column) {
          return column.active;
        });
        return _.map(columns, 'name');
      };

      function getIndexOfColumn(name) {
        console.log($scope.columns, _.findIndex($scope.columns, { name: name }));
        return _.findIndex($scope.columns, { name: name });
      };

      $scope.imitate = function() {
        var request = {
          filename: $scope.file,
          columns: getSelectedColumns(),
          plotColumns: [$scope.plotColumns.x, $scope.plotColumns.y]
        };

        Socket.emit('csv/imitate', request);
      };
    }
  };
});
