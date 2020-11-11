function get_date(year_month) {
    const month30 = [4,6,9,11];
    const month31 = [1,3,5,7,8,10,12];
    let result = year_month.replace('/','-');
    const month = parseInt(year_month.slice(-2));
    if (month30.includes(month)) {
        result += '-30'
    } else if (month31.includes(month)) {
        result += '-31'
    } else if (month === 2) {
        result += '-28'
    }
    return result;
}

function clone_element(element) {
    kit_num = '';
    if (element.id.split('_')[0].includes('k')) {
        kit_num = element.split('_')[0]+ '_';
    }
    let counter = parseInt(document.getElementById(kit_num + 'comps').lastElementChild.id.slice(4)) + 1;

    const div_num = element.id.substr(-1);
    const div = document.getElementById(kit_num + 'comp' + div_num);
    for (let k = 0; k < document.getElementById(kit_num + 'copy_num' + div_num).value; k++) {
        const clone = div.cloneNode(true);
        clone.id = clone.id.slice(0, -1) + counter.toString();
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

function remove_element(element) {
    const containerDiv = element.parentElement.parentElement.parentElement.id;
    document.getElementById(containerDiv).remove();
}

function enable(element) {
    properties = element.value.split(',');

    update();
    const raw_comps = document.getElementById('containers_div');
    if (raw_comps != null) {
        raw_comps.childNodes.forEach(function (element) {
            if (element.tagName == 'DIV') {
                update_comp(element.id.slice(-1));
            }
        });
    }
}

function confirmMsg() {
    return confirm('Are you sure?');
}

function deleteMsg(deletable) {
    if (deletable == 'True') {
        return confirmMsg();
    } else {
        alert('This cannot be deleted.');
        return false;
    }
}

function editMsg(deletable) {
    if (deletable == 'True') {
        return true;
    } else {
        alert('This cannot be edited.');
        document.getElementById('edit_btn').setAttribute('data-target','#None')
        return false;
    }
}
