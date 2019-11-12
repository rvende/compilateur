function printx(x){
	if(x != 0){
		printx(x/10);
		var b;
		b = x%10 + 48;
		send b;
	}
}

function print(y){
	if(y == 0){
		send 40;
	}else{
		printx(y);
	}
	send 10;
}

function somme(n,m,k){ 
	if(n<=0){ 
		return 2+m+k;  
	}else{ 
		if(n == 15){ 
			return n;
		}
			
			var i; 
			for(i =0;i<3;i=i+1){ 
				n = n-1; 
				if(n == 12){ 
					break;
			 	}
			} 
		return n*m+k + somme(n-1,m,k-1) + k -2; 
		
	} 
} 
function main() { 
	var a; 
	a = 2; 
	a = a+ somme(22,4,2); 
	send a;
	return a;
}
