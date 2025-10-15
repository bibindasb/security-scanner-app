// frontend/src/components/findings/FindingList.jsx
import React, { useState } from 'react';
import {
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Chip,
  Pagination,
} from '@mui/material';
import FindingCard from './FindingCard';

const FindingList = ({ findings, onAnalyzeFinding }) => {
  const [severityFilter, setSeverityFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const itemsPerPage = 10;

  const filteredFindings = findings.filter(finding => {
    const matchesSeverity = severityFilter === 'all' || finding.severity === severityFilter;
    const matchesType = typeFilter === 'all' || finding.type === typeFilter;
    const matchesSearch = finding.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         finding.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesSeverity && matchesType && matchesSearch;
  });

  const paginatedFindings = filteredFindings.slice(
    (page - 1) * itemsPerPage,
    page * itemsPerPage
  );

  const severityCounts = {
    all: findings.length,
    critical: findings.filter(f => f.severity === 'critical').length,
    high: findings.filter(f => f.severity === 'high').length,
    medium: findings.filter(f => f.severity === 'medium').length,
    low: findings.filter(f => f.severity === 'low').length,
    info: findings.filter(f => f.severity === 'info').length,
  };

  return (
    <Box>
      {/* Filters */}
      <Box sx={{ mb: 3, display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center' }}>
        <TextField
          size="small"
          placeholder="Search findings..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{ minWidth: 200 }}
        />
        
        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Severity</InputLabel>
          <Select
            value={severityFilter}
            label="Severity"
            onChange={(e) => setSeverityFilter(e.target.value)}
          >
            {Object.entries(severityCounts).map(([value, count]) => (
              <MenuItem key={value} value={value}>
                {value.charAt(0).toUpperCase() + value.slice(1)} ({count})
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Type</InputLabel>
          <Select
            value={typeFilter}
            label="Type"
            onChange={(e) => setTypeFilter(e.target.value)}
          >
            <MenuItem value="all">All Types</MenuItem>
            <MenuItem value="vulnerability">Vulnerability</MenuItem>
            <MenuItem value="misconfiguration">Misconfiguration</MenuItem>
            <MenuItem value="information">Information</MenuItem>
          </Select>
        </FormControl>

        <Chip
          label={`${filteredFindings.length} findings`}
          color="primary"
          variant="outlined"
        />
      </Box>

      {/* Findings List */}
      {paginatedFindings.length === 0 ? (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography color="textSecondary">
            No findings match your filters
          </Typography>
        </Box>
      ) : (
        <>
          {paginatedFindings.map((finding) => (
            <FindingCard
              key={finding.id}
              finding={finding}
              onAnalyze={onAnalyzeFinding}
            />
          ))}
          
          {/* Pagination */}
          {filteredFindings.length > itemsPerPage && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
              <Pagination
                count={Math.ceil(filteredFindings.length / itemsPerPage)}
                page={page}
                onChange={(e, value) => setPage(value)}
                color="primary"
              />
            </Box>
          )}
        </>
      )}
    </Box>
  );
};

export default FindingList;