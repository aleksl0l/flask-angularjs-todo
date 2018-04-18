var app = angular.module('todoApp', ['ngResource']);

app.controller('todoCtrl', function($scope, $resource) {

    $scope.addTask = function()
    {
        var new_todo = $resource('http://127.0.0.1:5000/add', {description: $scope.newTask}, {add:{method:'POST'}});
        new_todo.add();
        $scope.get_todos();
        $scope.newTask = "";
    }

    $scope.get_todos = function()
    {
        var todos = $resource('http://127.0.0.1:5000/get_all_todos');
        todos.get({}, function(response) {
            $scope.data = response['result'];
        });
    }
    $scope.get_todos();


    $scope.delete = function(id)
    {
        var del = $resource('http://127.0.0.1:5000/:id_todo', {id_todo: id}, {del: {method:'DELETE'}})
        del.del();
        $scope.get_todos();
     }

     $scope.modify = function(id)
    {
        var mod = $resource('http://127.0.0.1:5000/:id_todo', {id_todo: id}, {mod: {method:'PUT'}})
        mod.mod();
        $scope.get_todos();
     }
});