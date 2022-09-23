import { useState, useEffect } from 'react';


/**
 * component for raw data
 * @param {object} props 
*/
export default function RawJSON(props) {
  const {raws} = props;

  const [selectedIndex, setSelectedIndex] = useState(0);
  const [content, setContent] = useState();

  useEffect( () => {
    raws && fetch(
      raws[selectedIndex]["file"],
      {
        headers : { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
         }
      }
    )
    .then( (response) => {
      if (response.ok) {
        return response.json();
      }
      throw new Error("Content not found!");
    })
    .then(json => setContent(json))
    .catch((err) => {
      setContent(null);
    })},
    [selectedIndex, raws]
  );

  if (!raws) {
    return (
      <div className="no-data">
        <p><strong>Oops! No data to display.</strong></p>
      </div>
    )
  }

  return (
    <div className="raws-container">
      <div className="sidebar">
        <ul>
          {raws.map( (item, index) => (
            <li
              key={index}
              className={selectedIndex===index ? "selected": null}
              onClick={() => setSelectedIndex(index)}
            >
              {item.label}
            </li>
          ))}

        </ul>
      </div>
      <div className="selected-raw">
        <pre>{JSON.stringify(content, null, 2)}</pre>
      </div>
    </div>
  );
}