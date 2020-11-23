let properties = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

function update_all(element) {
    properties = element.value.split(',');
    update_barcode(element);
    const comps = document.getElementById('comps').childNodes;
    comps.forEach(function (element) {
        if (element.tagName === 'FIELDSET') {
            update_comp(element);
        }
    });

}

function update_barcode() {
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
