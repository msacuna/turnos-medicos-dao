import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import '../../styles/back_button.css';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

const BackButton = () => {
  const navigate = useNavigate();
  return (
    <Button className="back-button" onClick={() => navigate(-1)} title="Volver">
      <ArrowBackIcon
        className="back-icon" // Ajusta el tamaño y color
      />
    </Button>
  );
};
export default BackButton;
