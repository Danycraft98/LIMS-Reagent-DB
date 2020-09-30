let counter = 1;
let properties = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

function add_kit() {
    var container = document.getElementById("kits")
    var index = container.children.length / 2

    var cln = document.getElementById("add_kit").cloneNode(true);
    cln.children[0].children[0].setAttribute("data-target", "#kit" + index);
    cln.children[0].children[0].removeAttribute("hidden");
    cln.children[1].children[0].remove();
    container.appendChild(cln);

    // Copy the element and its child nodes
    cln = document.getElementById("kit0").cloneNode(true);
    cln.querySelectorAll("[id^='k0']").forEach(function(element, test) {
        /*if (element.id.includes("name")) {
            element.setAttribute("required","");
        }*/
        element.name = element.name.replace(/^k\d/gi, 'k' + index)
        element.id = element.id.replace(/^k\d/gi, 'k' + index)
    })
    cln.id = "kit" + index
    cln.removeAttribute("hidden")
    container.appendChild(cln);
}

function clone_element(element) {
    var kit_num = element.id.split("_")[0];
    let counter = parseInt(document.getElementById(kit_num + '_comps').lastElementChild.id.slice("p")[1]) + 1;

    const div_num = element.id.substr(-1);
    const div = document.getElementById(kit_num + '_comp' + div_num);
    for (let k = 0; k < document.getElementById(kit_num + '_copy_num' + div_num).value; k++) {
        const clone = div.cloneNode(true);
        clone.id = clone.id.slice(0, -1) + counter.toString();
        var nodeList = clone.childNodes;
        clone.childNodes.forEach(function (element) {
            if (element.tagName == 'DIV') {
                element.childNodes.forEach(function (sub_element, index, parent) {
                    if (sub_element.childNodes.length > 3) {
                        let input = sub_element.childNodes;
                        if (input[1].tagName != 'LABEL') {
                            input[1].id = input[1].id.slice(0, -1) + counter.toString();
                        }
                        if (input[3] != undefined) {
                            input[3].id = input[3].id.slice(0, -1) + counter.toString();
                        }
                    }
                });
            }
        });

        clone.removeAttribute('hidden');
        document.getElementById(kit_num + "_comps").appendChild(clone);
        counter++;
    }
}

function update_all(element) {
    var kit_num = element.id.split("_")[0];
    properties = element.value.split(",");
    update_barcode(element);
    const comps = document.getElementById(kit_num + '_comps').childNodes;
    comps.forEach(function (element) {
        if (element.tagName == 'FIELDSET') {
            update_comp(element);
        }
    });

}

function update_barcode(element) {
    var kit_num = element.id.split("_")[0];
    const barcode = document.getElementById(kit_num + "_barcode").value;
    if (properties[1] >= 0) {
        document.getElementById(kit_num + "_part_num").setAttribute("value", barcode.slice(properties[1], properties[2]));
    } else {
        document.getElementById(kit_num + "_part_num").setAttribute("value", "");
    }

    if (properties[3] >= 0) {
        document.getElementById(kit_num + "_lot_num").setAttribute("value", barcode.slice(properties[3], properties[4]));
    } else {
        document.getElementById(kit_num + "_lot_num").setAttribute("value", "");
    }

    if (properties[5] >= 0) {
        document.getElementById(kit_num + "_exp_date").setAttribute("value", get_date(barcode.slice(properties[5], properties[6])));
    } else {
        document.getElementById(kit_num + "_exp_date").setAttribute("value", "");
    }
}

function update_comp(element) {
    var kit_num = element.id.split("_")[0];
    const barcode = document.getElementById(kit_num + "_comp_barcode" + element.id.slice(-1)).value;

    if (properties[7] >= 0) {
        document.getElementById(kit_num + "_part_num" + element.id.slice(-1)).setAttribute("value", barcode.slice(properties[7], properties[8]));
    } else {
        document.getElementById(kit_num + "_part_num" + element.id.slice(-1)).setAttribute("value", "");
    }

    if (properties[9] >= 0) {
        document.getElementById(kit_num + "_lot_num" + element.id.slice(-1)).setAttribute("value", barcode.slice(properties[9], properties[10]));
    } else {
        document.getElementById(kit_num + "_lot_num" + element.id.slice(-1)).setAttribute("value", "");
    }
}
