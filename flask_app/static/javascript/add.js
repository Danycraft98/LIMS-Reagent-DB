function checkbox_pressed(element) {
	document.getElementById(element.id.slice(0,-3)+"_btn").disabled = !element.checked;
	document.getElementById(element.id.slice(0,-3)).setAttribute("value","")
}

var counter = 1;
var properties;
function add_element() {
	var tag = document.createElement("div");
	tag.setAttribute("id", "container_div"+counter)
	tag.setAttribute("style", "padding-bottom:30px")
	tag.innerHTML = '<div class="row my-row"> <div class="col-3 form-group"> <label for="comp_name'+counter+'">Component Name:</label> <input type="text" class="form-control" name="comp_name" id="comp_name'+counter+'"> </div> <div class="col-4 form-group"> <label for="comp_barcode'+counter+'">Component Barcode:</label> <input type="text" class="form-control" name="comp_barcode" id="comp_barcode'+counter+'" oninput="update_comp(this)"> </div> <div class="col-3 form-group"> </div> <div class="col-2 form-group"> <label for="comp_barcode'+counter+'" style="visibility: hidden;">Traaaaaaaaaaash:</label> <button type="button" class="btn btn-default" name="clone" id="clone" onclick="clone_element(this)"> <i class="fa fa-clone" style="font-size:24px"></i> </button> <button type="button" class="btn btn-default" name="trash" id="trash'+counter+'" onclick="remove_element(this)"> <i class="fa fa-trash-o" style="font-size:24px"></i> </button> </div> </div> <div class="row my-row"> <div class="col-3 form-group"> <label for="comp_part_num'+counter+'">Part Number:</label> <input type="text" class="form-control" name="comp_part_num" id="comp_part_num'+counter+'"> </div> <div class="col-3 form-group"> <label for="comp_lot_num'+counter+'">Lot Number:</label> <input type="text" class="form-control" name="comp_lot_num" id="comp_lot_num'+counter+'"> </div> <div class="col-6 form-group"> <label for="condition'+counter+'">Component Condition:</label> <input type="text" class="form-control" name="condition" id="condition'+counter+'"> </div> </div>';
	document.getElementById("containers_div").appendChild(tag);
	counter++;
}

function clone_element(element) {
	var containerDiv = element.parentElement.parentElement.parentElement.id
	for (k = 0; k < document.getElementById('copy_num').value; k++) {
		var clone = document.getElementById(containerDiv).cloneNode(true);
		clone.id = containerDiv + counter;
		document.getElementById("containers_div").appendChild(clone);
		var nodeList = clone.childNodes;
		for (i = 0; i < nodeList.length; i++) {
			if (nodeList[i].tagName == 'DIV') {
				var subNodeList = nodeList[i].childNodes;
				for (j = 0; j < subNodeList.length; j++) {
					if (subNodeList[j].childNodes[3] != undefined) {
						var id = subNodeList[j].childNodes[3].id;
						subNodeList[j].childNodes[3].id = id.substring(0,id.length-1) + counter;
					}
				}
			}
		}
		counter++;
	}
}

function remove_element(element) {
	var containerDiv = element.parentElement.parentElement.parentElement.id
	document.getElementById(containerDiv).remove();
}

function enable(element) {
	properties = element.value.split(",");
	if (properties[2] == 1) {
		$("#exp_date").prop("disabled", false);
	} else {
		$("#exp_date").prop("disabled", true);
		document.getElementById("exp_date").setAttribute("value","");
	}
	update()
	comps = document.getElementById("containers_div").childNodes;
	for (i = 0; i < comps.length; i++) {
		if (comps[i].tagName == 'DIV') {
			update_comp(comps[i].childNodes[1].childNodes[3].childNodes[3])
		}
	}
}

function update() {
	if (properties[0] == 1) {
		document.getElementById("part_num").setAttribute("value", document.getElementById("barcode").value.slice(properties[3], properties[4]));
	} else {
		document.getElementById("part_num").setAttribute("value", "");
	}
	if (properties[1] == 1) {
		document.getElementById("lot_num").setAttribute("value", document.getElementById("barcode").value.slice(properties[5], properties[6]));
	} else {
		document.getElementById("lot_num").setAttribute("value", "");
	}

	if (document.getElementById("exp_date").disabled == false) {
		document.getElementById("exp_date").setAttribute("value",document.getElementById("barcode").value.slice(properties[7], properties[8]).replace(/\//g, "-") +"-28");
	}
}

function update_comp(element) {
	console.log(properties)
	if (properties[9] == 1) {
		element.disabled = false;
	} else {
		element.disabled = true;
	}
	if (properties[10] == 1) {
	      document.getElementById("comp_part_num"+element.id.substr(-1)).disabled = false;
		document.getElementById("comp_part_num"+element.id.substr(-1)).setAttribute("value", element.value.slice(properties[12], properties[13]));
	} else {
		document.getElementById("comp_part_num"+element.id.substr(-1)).setAttribute("value", "");
		document.getElementById("comp_part_num"+element.id.substr(-1)).disabled = true;
	}

	if (properties[11] == 1) {
	    document.getElementById("comp_lot_num"+element.id.substr(-1)).disabled = false;
		document.getElementById("comp_lot_num"+element.id.substr(-1)).setAttribute("value", element.value.slice(properties[14], properties[15]));
	} else {
		document.getElementById("comp_lot_num"+element.id.substr(-1)).setAttribute("value", "");
		document.getElementById("comp_lot_num"+element.id.substr(-1)).disabled = true;
	}
}

function confirmMsg() {
	if (confirm("Are you sure?")) {
		return true;
	} else {
		return false;
	}
}