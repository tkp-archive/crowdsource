function toggle_active_view(which){
    for(let x of document.getElementsByClassName('active-competition')){
        x.style.display = which ? 'block': 'none';
    }
    for(let x of document.getElementsByClassName('inactive-competition')){
        x.style.display = which ? 'none': 'block';
    }
}