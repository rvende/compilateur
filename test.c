function somme(n){ 
	if(n<=0){ 
		return 2; 
	}else{ 
		return n + somme(n-1); 
	} 
} 

<<<<<<< HEAD
function main(){ 
	var a; 
	a = 2; 
	a = a+ somme(22); 
	send a;
	return a;
}
=======
function ab(a,b){
	var res;
	res = a+b;
	return res;
}

function main() {
	var mres;
	mres = ab(1, 2);
  var i;
  for (i = 0; i < 5; i = i + 1) {
  }
	return i;
}
>>>>>>> f5c04584baa36e8232661296a5fef290b4f002f1
