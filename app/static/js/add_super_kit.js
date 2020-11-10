function edit_button(element) {
    if (element.innerText.includes('Add')) {
        element.innerText = 'Delete Super Kit'
    } else {
        element.innerText = 'Add Super Kit'
        $('input[name=sk_name').val('');
    }

    const div = document.getElementById('edit_button_div');
    if (div.className.includes('mt-5')) {
        div.setAttribute('class', 'row mt-3 mb-3');
    } else {
        div.setAttribute('class', 'row mt-5 mb-3');
    }
}

function collapse(element) {
    var arrow = element.firstChild;
    if (element.innerText.includes('Expand')) {
        arrow.className = arrow.className.replace('down', 'up');
        element.innerHTML = element.innerHTML.replace('Expand', 'Collapse');
    } else {
        arrow.className = arrow.className.replace('up', 'down');
        element.innerHTML = element.innerHTML.replace('Collapse', 'Expand');
    }
}

function get_kit_ids() {
    kit_ids = document.getElementById('kit_ids')
    kit_ids.value = ''
    document.getElementById('kits').childNodes.forEach(function(element) {
        if (element.id && !isNaN(element.id.slice(3)) && !element.id.includes('0')) {
            if (kit_ids.value != '')
                kit_ids.value += ','
            kit_ids.value += element.id.slice(3)
        }
    })
}

function delete_kit(element) {
    var kit_element = document.getElementById('kit' + element.id.slice(1));
    kit_element.previousSibling.remove();
    kit_element.remove();
    get_kit_ids();
}

let counter = 1;
let properties = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

function add_kit() {
    var container = document.getElementById('kits')
    var index = parseInt(container.lastElementChild.id.slice(3), 10) + 1

    var cln = document.getElementById('add_kit').cloneNode(true);
    cln.children[0].children[0].setAttribute('data-target', '#kit' + index);
    cln.children[0].children[0].removeAttribute('hidden');
    cln.children[1].children[0].remove();
    container.appendChild(cln);

    // Copy the element and its child nodes
    cln = document.getElementById('kit0').cloneNode(true);
    cln.querySelectorAll("[id^='k0']").forEach(function(element, test) {
        if (element.id.includes('exp_date') && !element.name.includes('comp')) {
            element.setAttribute('required','');
        }
        element.name = element.name.replace(/^k\d/gi, 'k' + index)
        element.id = element.id.replace(/^k\d/gi, 'k' + index)
    })
    cln.id = 'kit' + index
    cln.removeAttribute('hidden')
    container.appendChild(cln);
    get_kit_ids();
}

function clone_element(element) {
    var kit_num = element.id.split('_')[0];
    let counter = parseInt(document.getElementById(kit_num + '_comps').lastElementChild.id.split('p')[1]) + 1;

    const div_num = element.id.split('p')[1];
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
        document.getElementById(kit_num + '_comps').appendChild(clone);
        counter++;
    }
}

function update_all(element) {
    var kit_num = element.id.split('_')[0];
    properties = element.value.split(',');
    update_barcode(element);
    const comps = document.getElementById(kit_num + '_comps').childNodes;
    comps.forEach(function (element) {
        if (element.tagName == 'FIELDSET') {
            update_comp(element);
        }
    });

}

function update_barcode(element) {
    var kit_num = element.id.split('_')[0];
    const barcode = document.getElementById(kit_num + '_barcode').value;
    if (properties[1] >= 0) {
        document.getElementById(kit_num + '_part_num').setAttribute('value', barcode.slice(properties[1], properties[2]));
    } else {
        document.getElementById(kit_num + '_part_num').setAttribute('value', '');
    }

    if (properties[3] >= 0) {
        document.getElementById(kit_num + '_lot_num').setAttribute('value', barcode.slice(properties[3], properties[4]));
    } else {
        document.getElementById(kit_num + '_lot_num').setAttribute('value', '');
    }

    if (properties[5] >= 0) {
        document.getElementById(kit_num + '_exp_date').setAttribute('value', get_date(barcode.slice(properties[5], properties[6])));
    } else {
        document.getElementById(kit_num + '_exp_date').setAttribute('value', '');
    }
}

function update_comp(element) {
    var kit_num = element.id.split('_')[0] + '_';
    const barcode = document.getElementById(kit_num + 'comp_barcode' + element.id.slice(-1)).value;

    if (properties[7] >= 0) {
        document.getElementById(kit_num + 'part_num' + element.id.slice(-1)).setAttribute('value', barcode.slice(properties[7], properties[8]));
    } else {
        document.getElementById(kit_num + 'part_num' + element.id.slice(-1)).setAttribute('value', '');
    }

    if (properties[9] >= 0) {
        document.getElementById(kit_num + 'lot_num' + element.id.slice(-1)).setAttribute('value', barcode.slice(properties[9], properties[10]));
    } else {
        document.getElementById(kit_num + 'lot_num' + element.id.slice(-1)).setAttribute('value', '');
    }
}
