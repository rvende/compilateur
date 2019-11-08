
function ab(a,b){
	var res;
	res = a+b;
	return res;
}

function main() {
	var mres;
	mres = ab(1, 2);
  var i;
  var j;
  for (i = 0; i < 5; i = i + 1) {
    for (j = 0; j < 5; j = j + 1) {
      if(j==2){
        break;
      }
    }
  }
	return mres;
}
