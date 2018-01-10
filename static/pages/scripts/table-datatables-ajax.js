var TableDatatablesAjax = function () {

    var handleDemo1 = function () {

        var grid = new Datatable();

        grid.init({
            src: $("#datatable_ajax"),
            onSuccess: function (grid, response) {
                // grid:        grid object
                // response:    json object of server side ajax response
                // execute some code after table records loaded
            },
            onError: function (grid) {
                // execute some code on network or other general error
            },
            onDataLoad: function(grid) {
                // execute some code on ajax data load
            },
            loadingMessage: 'Loading...',
            dataTable: { // here you can define a typical datatable settings from http://datatables.net/usage/s

                "dom": "<'row'<'col-md-3 col-sm-12'<'#uc.pull-left'>><'col-md-6 col-sm-12 text-center'l><'col-md-3 col-sm-12'f>r>t<'row'<'col-md-3 col-sm-12'<'table-group-actions text-left'>><'col-md-6 col-sm-12  text-center 'i><'col-md-3 col-sm-12 text-right'p>>",
                // save datatable state(pagination, sort, etc) in cookie.
                "bStateSave": true,

                 // save custom filters to the state
                "fnStateSaveParams":    function ( oSettings, sValue ) {
                    $("#datatable_ajax tr.filter .form-control").each(function() {
                        sValue[$(this).attr('name')] = $(this).val();
                    });

                    return sValue;
                },

                // read the custom filters from saved state and populate the filter inputs
                "fnStateLoadParams" : function ( oSettings, oData ) {
                    //Load custom filters
                    $("#datatable_ajax tr.filter .form-control").each(function() {
                        var element = $(this);
                        if (oData[element.attr('name')]) {
                            element.val( oData[element.attr('name')] );
                        }
                    });

                    return true;
                },

                "lengthMenu": [
                    [10, 20, 50, 100, 150, -1],
                    [10, 20, 50, 100, 150, "All"] // change per page values here
                ],
                "pageLength": 50, // default record count per page
                "ajax": {
                    "type": "GET",
                    //"url": "http://192.168.255.130/table_ajax.php?length=15", // ajax source
                    "url": "http://123.207.14.42:8000/api/users/v1/users/"
                },
                "columns": [{data: "id"}, {data: "name" }, {data: "username" }, {data: "get_role_display" }, {data: "is_valid" }],
                "ordering": false,
                "order": [
                    [1, "asc"]
                ],// set first column as a default sort by asc
				"language": {
                    "loadingRecords": "Please wait ...",
                    "zeroRecords": "No records",
                    "emptyTable": "No data available in table",
                    "info": "Showing _START_ to _END_ of _TOTAL_ entries",
					"lengthMenu": "View _MENU_ records",

                },

                "retrieve": true
            }
        });

        // handle group actionsubmit button click
        grid.getTableWrapper().on('click', '.table-group-action-submit', function (e) {
            e.preventDefault();
            var action = $(".table-group-action-input", grid.getTableWrapper());
            if (action.val() != "" && grid.getSelectedRowsCount() > 0) {
                grid.setAjaxParam("customActionType", "group_action");
                grid.setAjaxParam("customActionName", action.val());
                grid.setAjaxParam("id", grid.getSelectedRows());
                grid.getDataTable().ajax.reload();
                grid.clearAjaxParams();
            } else if (action.val() == "") {
                App.alert({
                    type: 'danger',
                    icon: 'warning',
                    message: 'Please select an action',
                    container: grid.getTableWrapper(),
                    place: 'prepend'
                });
            } else if (grid.getSelectedRowsCount() === 0) {
                App.alert({
                    type: 'danger',
                    icon: 'warning',
                    message: 'No record selected',
                    container: grid.getTableWrapper(),
                    place: 'prepend'
                });
            }
        })

        var uc_html = '<div class="uc pull-left m-l-5 m-r-5"><a href="www.baidu.com" class="btn sbold green"> 新建用户 <i class="fa fa-plus"></i></a></div>'
		grid.getDataTable().on('draw', function(){
                 $('#uc').html(uc_html);
		});
    }

    return {
        init: function () {
            handleDemo1();
        }
    };
}();

jQuery(document).ready(function() {
    TableDatatablesAjax.init();
    });