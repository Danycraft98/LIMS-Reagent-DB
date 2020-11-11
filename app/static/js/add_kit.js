function edit_button(element) {
    if (element.innerText.includes('Add')) {
        element.innerText = 'Delete Super Kit'
    } else {
        element.innerText = 'Add Super Kit'

        $('input[name=sk_name]').val('');
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

let counter = 1;
let properties = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

function clone_element(element) {
    let counter = parseInt(document.getElementById('comps').lastElementChild.id.split('p')[1]) + 1;
    let div_num;
    if (element.id.includes('comp')) {
        div_num = element.id.split('p')[1];
    } else {
        div_num = element.id.split('e')[1];
    }
    const div = document.getElementById('comp' + div_num);
    for (let k = 0; k < document.getElementById('copy_num' + div_num).value; k++) {
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
        document.getElementById('comps').appendChild(clone);
        counter++;
    }
}

function update_all(element) {
    var kit_num = element.id.split('_')[0];
    properties = element.value.split(',');
    update_barcode(element);
    const comps = document.getElementById('comps').childNodes;
    comps.forEach(function (element) {
        if (element.tagName == 'FIELDSET') {
            update_comp(element);
        }
    });

}

function update_barcode(element) {
    const barcode = document.getElementById('barcode').value;
    if (properties[1] >= 0) {
        document.getElementById('part_num').setAttribute('value', barcode.slice(properties[1], properties[2]));
    } else {
        document.getElementById('part_num').setAttribute('value', '');
    }

    if (properties[3] >= 0) {
        document.getElementById('lot_num').setAttribute('value', barcode.slice(properties[3], properties[4]));
    } else {
        document.getElementById('lot_num').setAttribute('value', '');
    }

    if (properties[5] >= 0) {
        document.getElementById('exp_date').setAttribute('value', get_date(barcode.slice(properties[5], properties[6])));
    } else {
        document.getElementById('exp_date').setAttribute('value', '');
    }
}

function update_comp(element) {
    const barcode = document.getElementById('comp_barcode' + element.id.slice(-1)).value;

    if (properties[7] >= 0) {
        document.getElementById('part_num' + element.id.slice(-1)).setAttribute('value', barcode.slice(properties[7], properties[8]));
    } else {
        document.getElementById('part_num' + element.id.slice(-1)).setAttribute('value', '');
    }

    if (properties[9] >= 0) {
        document.getElementById('lot_num' + element.id.slice(-1)).setAttribute('value', barcode.slice(properties[9], properties[10]));
    } else {
        document.getElementById('lot_num' + element.id.slice(-1)).setAttribute('value', '');
    }
}
