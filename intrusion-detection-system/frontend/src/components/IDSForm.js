import React, { useState } from 'react';
import axios from 'axios';
import './IDSForm.css'; // Create this CSS file for styling

const IDSForm = () => {
  const [formData, setFormData] = useState({
    protocol_type: '',
  service: '',
  flag: '',
  src_bytes: '',
  dst_bytes: '',
  count: '',
  same_srv_rate: '',
  diff_srv_rate: '',
  dst_host_srv_count: '',
  dst_host_same_src_port_rate: '',
  });

  const [result, setResult] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const res = await axios.post('http://10.66.21.150:5000/predict', formData);

      setResult(res.data.prediction);
    } catch (err) {
      console.error(err);
      setResult('Error occurred during prediction.');
    }
  };

  return (
    <div className="form-container">
      <h2>Intrusion Detection Prediction</h2>
      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          <div key={key} className="form-group">
            <label>{key.replace(/_/g, ' ').toUpperCase()}</label>
            <input
              type="text"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              required
            />
          </div>
        ))}

        <button type="submit">Predict</button>
      </form>
      {result && <h3>Prediction Result: {result}</h3>}
    </div>
  );
};

export default IDSForm;
