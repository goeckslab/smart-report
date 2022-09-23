
/**
 * component for Images
 * @param {object} props 
 */
export default function Images(props) {
  const {images} = props;
  return (
    <div className="images-container">
      {images.map((im, ix) => (
          <img loading="lazy" key={ix} src={im.file} alt={im.label}/>
      ))}
    </div>
  );
}