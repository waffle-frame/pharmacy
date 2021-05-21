$ = function (val ){
    let result;
    if (document.querySelectorAll(val).length <= 1){
        result = document.querySelector(val);

        result.text= function(vals) {
                        this.innerHTML =vals;
                        };
        result.val= function(vals) {
                        this.value = (vals) ? vals : "";
                        return  this.value;
                    };
    }
    else
    {
        result = document.querySelectorAll(val);
        result.click = function(  function_name ){
                            this.forEach( function(e, index){
                                e.addEventListener("click",  function_name);
                            });
                        }
    }
    return result;
}
function calculate( temp )
{
let result,
    expression,
    output;

if((!isNaN(temp["val1"])) && temp["opt"]   !==  "undefined" )
{
    temp["val2"] =  (!isNaN(temp["val2"])) ? temp["val2"] : temp["val1"];
    expression = temp["val1"]+""+ temp["opt"]+""+temp["val2"];
    result = eval( expression);
    output = [ result , expression];
}
else {
    output = [0 ,0];
}
return  output ;
}
function isOverflow (ele)
{

if((ele.scrollWidth -ele.clientWidth) >10 ) {
    if(((ele.scrollWidth -ele.clientWidth) /10) < 1.8 )
    {
        ele.style.fontSize = ((ele.scrollWidth -ele.clientWidth) /10) + "em";
    }
}
}

var temp  = [];
$("button").click(function (e) {
var val,
    opt,
    result,
    inputText,
    expOut;

val = parseInt(e.target.value );
opt =  e.target.value;

inputText = $("input");
expOut  = $("#temp");

if(isNaN(val))
{
    if(opt === "=")
    {
        result = calculate(temp);

        expOut.text(result[1]);
        inputText.val(""+result[0]);
        temp["val1"] = result[0];
        temp.splice("val2", 1);

    }
    else
    {
        if(opt !== 'c')
        {
            temp["opt"] = opt;
            expOut.text(inputText.value+= ""+opt);
            inputText.val( "");
        }
        else
        {
            temp = [];
            expOut.text("");
            inputText.val( "");
        }
    }
}
else
{
    inputText.value+= val;
    if(temp["opt"])
    {
        temp["val2"]= inputText.value;
    }
    else
    {
        temp["val1"]= inputText.value;
    }

}
isOverflow(inputText);
});



$('#calculator-call').addEventListener('click', () => {
    document.getElementById('calculator-block').innerHTML = `
    <div class="cal">
        <p id="temp"></p>
        <div class="content">
            <input class="calc-input" type="text">
            <div class="calc-btns">
                <button value="1">1</button>
                <button value="2">2</button>
                <button value="3">3</button>
                <button value="+">+</button>
                <button value="4">4</button>
                <button value="5">5</button>
                <button value="6">6</button>
                <button value="-">-</button>
                <button value="7">7</button>
                <button value="8">8</button>
                <button value="9">9</button>
                <button value="*">x</button>
                <button value="0">0</button>
                <button value="c">C</button>
                <button value="/">/</button>
                <button value="=">=</button>
            </div>
        </div>
    </div>`
})