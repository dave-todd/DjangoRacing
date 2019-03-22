import React, {Component} from 'react';
import {ScrollView, ActivityIndicator, Alert, Platform, StyleSheet, Button, TextInput, Text, View} from 'react-native';

type Props = {};

class RwwaComponent extends Component<Props> {
	
	constructor(props) {
		super(props)
		this.state = { content : this.buildStartData() }
	}
	
	render() {
		return (
			<View style={styles.container}>
				<View style={styles.container}>
					<Text style={styles.welcome}>Python/Django API Consumer in JavaScript/ReactNative</Text>
					<Text style={styles.instructions}>Press the GO button to see meeting information for race 17553</Text>
					<Button onPress={this.onPressButton} title="GO"/>
				</View>
				{this.state.content}
			</View>
		);
	}
	
	onPressButton = () => {
		fetch('http://10.0.2.2:8000/app/process/17553', { method: 'GET' } )
			.then( (response) => response.json() )
			.then( (data) => 
		{ 
			this.setState({ content: this.buildData(data), });
		} )
			.catch((error) => { console.error(error); });
	}
	
	buildData(data) {
		let content = [];
		for (let raceIndex=1; raceIndex < data.raceCount+1; raceIndex++) {
			let race = data["race"+raceIndex];
			content.push( <Text style={styles.welcome}>RACE : {race.raceNumber}, Horses : {race.horseCount}</Text>);
			for (let horseIndex=1; horseIndex < race.horseCount+1; horseIndex++) {
				let horse = race["horse"+horseIndex];
				content.push( <Text style={styles.data}>{horse.horseName}</Text>);
			}
		}
		return ( 
			<View style={styles.bigContainer}>
				<Text style={styles.data}>Start Date : {data.startDate}</Text>
				<Text style={styles.data}>Events : {data.raceCount}</Text>
				<ScrollView>
					{content}
				</ScrollView>
			</View>
		);
	}
	
	buildStartData() {
		return ( 
			<View style={styles.bigContainer}>
				<Text style={styles.data}>NO DATA</Text> 
			</View>
		);
	}
	
}

const styles = StyleSheet.create({

  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  
  bigContainer: {
    flex: 3,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
  
  data: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
  
  input: {
    height: 40,
	width: 120,
	textAlign: 'center',
	borderColor: 'gray', 
	borderWidth: 1,
  },
  
});

export default RwwaComponent