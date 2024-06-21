// src/App.jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import axios from 'axios';
import DOMPurify from 'dompurify';

const UploadHighlights = () => {
  const [file, setFile] = useState(null);
  const [bookName, setBookName] = useState('');
  const [author, setAuthor] = useState('');
  const [year, setYear] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('book_name', bookName);
    formData.append('author', author);
    formData.append('year', year);

    try {
      const response = await axios.post('http://localhost:8000/v2/uploadHighlights', formData);
      alert(response.data.response);
    } catch (error) {
      console.error('Error uploading highlights:', error);
    }
  };

  return (
      <div>
        <h2>Upload Highlights</h2>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} required />
          <input type="text" placeholder="Book Name" value={bookName} onChange={(e) => setBookName(e.target.value)} required />
          <input type="text" placeholder="Author" value={author} onChange={(e) => setAuthor(e.target.value)} required />
          <input type="text" placeholder="Year" value={year} onChange={(e) => setYear(e.target.value)} required />
          <button type="submit">Upload</button>
        </form>
      </div>
  );
};

const FetchHighlights = () => {
  const [highlights, setHighlights] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/v2/fetchHighlights');
        console.log('HERE:: highlights:: ', response.data);
        setHighlights(response.data);
      } catch (error) {
        console.error('Error fetching highlights:', error);
      }
    };
    fetchData();
  }, []);

  return (<div>
        <h2>All Highlights</h2>
        <ul>
          {highlights.map((highlight, index) => (<li key={index}>
                <strong>{highlight[0]}</strong>: {highlight[3]}
                <br/>
              </li>))}
        </ul>
      </div>);
};

const SearchHighlights = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/v2/searchHighlights?query=${query}`);
      setResults(response.data);
    } catch (error) {
      console.error('Error searching highlights:', error);
    }
  };

  const createMarkup = (html) => {
    return {__html: DOMPurify.sanitize(html)};
  }
  return (
      <div>
        <h2>Search Highlights</h2>
        <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search query" />
        <button onClick={handleSearch}>Search</button>
        <ul>
          {results.map((result, index) => (<li key={index} dangerouslySetInnerHTML={createMarkup(result)}></li>))}
        </ul>
      </div>);
};

const App = () => {
  return (
      <Router>
        <div>
          <nav>
            <ul>
              <li><Link to="/">Home</Link></li>
              <li><Link to="/upload">Upload Highlights</Link></li>
              <li><Link to="/fetch">Fetch Highlights</Link></li>
              <li><Link to="/search">Search Highlights</Link></li>
            </ul>
          </nav>

          <Routes>
            <Route path="/" element={<h1>Welcome to Highlights App</h1>} />
            <Route path="/upload" element={<UploadHighlights />} />
            <Route path="/fetch" element={<FetchHighlights />} />
            <Route path="/search" element={<SearchHighlights />} />
          </Routes>
        </div>
      </Router>
  );
};

export default App;