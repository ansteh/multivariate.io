var app = angular.module('app', ['ngMaterial']);

app.factory('Socket', function(){
  return io();
});
