function somme(n){ 
	if(n<=0){ 
		return 2; 
	}else{ 
		return n + somme(n-1); 
	} 
} 


function main(){ 
	var a; 
	a = 2; 
	a = a+ somme(22);

	send a;

	return a;
}
