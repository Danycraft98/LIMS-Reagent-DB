function checkbox_pressed(element) {
	document.getElementById(element.id.slice(0,-3)+"_btn").disabled = !element.checked;
	document.getElementById(element.id.slice(0,-3)).setAttribute("value","")
}

var counter = 0
function clone_element(element) {
	var containerDiv = element.parentElement.parentElement.parentElement.id
	for (k = 0; k < document.getElementById('copy_num' + containerDiv.substr(-1)).value; k++) {
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
	update()
	raw_comps = document.getElementById("containers_div")
	if (raw_comps != null) {
	    comps = raw_comps.childNodes;
	    for (i = 0; i < comps.length; i++) {
		    if (comps[i].tagName == 'DIV') {
			    update_comp(comps[i].childNodes[1].childNodes[3].childNodes[3])
	    	}
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


	if (properties[2] == 1) {
		var date = document.getElementById("barcode").value.slice(properties[7], properties[8]).replace(/\//g, "-");
		var month = parseInt(date.slice(5,7), 10);
		var large_month = [1,3,5,7,8,10,12];
		if (large_month.includes(month)) {
		    document.getElementById("exp_date").setAttribute("value",date+"-31");
		} else if (month == 2) {
		    document.getElementById("exp_date").setAttribute("value",date+"-28");
		}  else {
		    document.getElementById("exp_date").setAttribute("value",date+"-30");
		}
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

function deleteMsg(deletable) {
	if (deletable == "True") {
	    if (confirm("Are you sure?")) {
            return true;
        } else {
            return false;
        }
	} else {
        alert("This cannot be deleted.");
	}
}