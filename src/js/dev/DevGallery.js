import React, { Component } from "react";
const axios = require('axios');

class DevGallery extends Component {

    constructor(props){
        super(props);
        this.state = {
          entries: [],
          isLoading: true
        };
        this.getEntries();
    }

    getEntries(){

        var self = this;
        axios.get('/api/dev')
        .then(function (response){
            self.setState({
                entries: response.data.dev,
                isLoading: false
            });
        })
        .catch(function (error){
            console.log(error);
        });

    }

    render(){

        var arrays = [], size = 3;

        var a = this.state.entries.slice()
        while (a.length > 0)
            arrays.push(a.splice(0, size));

        const gallery = <div>{arrays.map((entry) => <Row entries={entry}/>)}</div>;

        const loadingMessage = <p className="center-text text-no-select" >Loading...</p>;

        return this.state.isLoading ? loadingMessage : gallery;
    }

}

function Row(props){

    return (
        <div className="row text-no-select">
            {props.entries.map((entry) => <DevEntry entry={entry} key={entry.index} />)}
        </div>

    );

}

function DevEntry(props){
    return (

        <div className="pad-4 card">
            <h1>{props.entry.name}</h1>

			{props.entry.description.map((entry) => <p key={entry} >{entry}</p>)}

            <a href={props.entry.url} className="button full-width">View</a>
        </div>

    );
}

export default DevGallery;