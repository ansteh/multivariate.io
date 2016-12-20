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
      $scope.collection = [];

      $scope.getActiveColumns = function() {
        var column = _.find($scope.columns, { name: "Date"});
        if(column) column.active = false;
        // console.log($scope.columns);
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

      Socket.on('csv/imitate/data', function(simulated) {
        console.log(simulated);
        var realDataColumnsIndices = _.map($scope.getActiveColumns(), function(colum) {
          return _.findIndex($scope.columns, colum);
        });
        var data = _.map($scope.data, function(row) {
          return _.map(realDataColumnsIndices, function(index) {
            return row[index];
          });
        });

        $scope.collection = _.map(_.take($scope.getActiveColumns(), 3), function(column, columnIndex) {
          return {
            title: column.name,
            x_accessor: "x",
            y_accessor: "y",
            data: _.map(_.take(data, simulated.length), function(row, rowIndex) {
              return { x: row[columnIndex], y: simulated[rowIndex][columnIndex] }
            })
          }
        });
        $scope.$apply();
      });

      $scope.fastImitate = function() {
        var request = {
          filename: $scope.file,
          columns: getSelectedColumns(),
          length: 500
        };
        console.log(request);
        Socket.emit('csv/imitate/data', request);
      };
    }
  };
});
