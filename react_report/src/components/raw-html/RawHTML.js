
/**
 * component for Images
 * @param {object} props 
 */
export default function RawHTML(props) {
  const {htmls} = props;
  return (
    <div className="raw-htmls-container">
      {htmls.map((html, ix) => (
        <iframe key={ix} src={html.file} alt={html.label} width="400" height="400"/>
      ))}
    </div>
  );
}