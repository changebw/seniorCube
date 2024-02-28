function Buttons() {

    const btn1 = <form action="/sendHighSig"><button id="lightOn">Turn Light On</button></form>;
    const btn2 = <form action="/sendLowSig"><button id="lightOff">Turn Light Off</button></form>;

    return <div>
            <h1>Hello</h1>
                {btn1}
                {btn2}
            </div>;
}

export default Buttons;