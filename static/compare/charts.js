var Graphics = {};

Graphics.scatter = function(anchor){

  var plot = function(options) {
    var data = options.data;

    var raw = _.map(options.data, options.y_accessor);
    var min_y = _.min(raw);
    var max_y = _.max(raw);

    MG.data_graphic({
      data: data,
      chart_type: 'point',
      animate_on_load: true,
      area: false,
      full_width: true,
      target: anchor,
      x_accessor: options.x_accessor,
      y_accessor: options.y_accessor,
      min_y: min_y,
      max_y: max_y,
    });
  };

  return {
    plot: plot
  };
};
