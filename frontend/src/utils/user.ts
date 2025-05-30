
function getUser():{email:string,name:string}|undefined {
    const user = localStorage.getItem("user") || undefined
    if(user){
        return JSON.parse(user)
    } 
    return undefined
    
}

export {getUser}