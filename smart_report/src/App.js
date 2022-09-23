import { useState } from 'react';
import { Images } from './components/images';
import { RawJSON } from './components/raw-json';
import { data } from './data';


import './App.css';


const App = () => {
  const {title, raws, images} = data;
  const tabs = ["Visualization", "Raw Data"];

  const [currentTab, setCurrentTab] = useState(0);

  return (
    <>
      <h2>{title}</h2>
      <div className="tabs">
        {tabs.map( (tab, ix) => (
          <button
            key={ix}
            className={"tab-button" + (currentTab===ix ? " active" : "")}
            onClick={() => setCurrentTab(ix)}
          >
            {tab}
          </button>
        ))}
      </div>
      {currentTab === 0
        ? <Images images={images} />
        : <RawJSON raws={raws}/>
      }
    </>
  );
}

export default App;