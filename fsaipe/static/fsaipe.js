(function(ns, $, undefined){

	var models = [];

	ns.include = function(model){
		models.push(model);
	}

	$(function(){
		if(typeof(base_url) === undefined){
			alert('Oops! Global `baseurl` não foi definida!');
		}

		$.each(models, function(){
			var name = this;
			$.get(base_url+'saipe/'+this+'/ajax/list', function(data){
				$("#saipe_table_"+name+" tr:last").after(data);
			}, 'html');
		});
	});
}( window.saipe = window.saipe || {}, jQuery ));
