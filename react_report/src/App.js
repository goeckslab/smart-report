import { useState } from 'react';
import { Images } from './components/images';
import { RawJSON } from './components/raw-json';
import { RawHTML } from './components/raw-html';
import { data } from './data';

import './App.css';


const App = () => {
  const {title, raws, images, htmls} = data;
  const tabs = ["Interactive Plot", "Visualization", "Raw Data"];

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
        ? <RawHTML htmls={htmls} />
        : (currentTab === 1
          ? <Images images={images} />
          : <RawJSON raws={raws}/>)
      }
    </>
  );
}

export default App;