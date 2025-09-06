import React from 'react';
import { Card, CardContent, Typography, List, ListItem, ListItemText, LinearProgress, Box } from '@mui/material';
import { ArrowRight, Info } from '@mui/icons-material';

const JointLKEnhancement = ({ dimport React from 'react';
import { Card, CardContent, Typography, List, ListItem, ListItemText, LinearProgress, Box } from '@mui/material';
import { ArrowRight, Info } from '@mui/icons-material';

const JointLKEnhancement = ({ data, isLoading }) => {
  if (isLoading) {
    return (
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            知识图谱增强推理中...
          </Typography>
          <LinearProgress />
        </CardContent>
      </Card>
    );
  }

  if (!data || !data.relevant_nodes || data.relevant_nodes.length === 0) {
    return null;
  }

  return (
    <Card sx={{ mb: 3, borderLeft: '4px solid #1976d2' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          <Info color="primary" sx={{ verticalAlign: 'middle', mr: 1 }} />
          知识图谱增强推理
        </Typography>

        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          与当前问题最相关的知识节点（由JointLK模型计算）：
        </Typography>

        <List dense>
          {data.relevant_nodes.map(([nodeId, nodeName], index) => (
            <React.Fragment key={nodeId}>
              <ListItem alignItems="center">
                <ListItemText
                  primary={nodeName}
                  secondary={`节点ID: ${nodeId}`}
                />
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Typography variant="body2" sx={{ mr: 1 }}>
                    {Math.round(data.confidence_scores[index] * 100)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={data.confidence_scores[index] * 100}
                    sx={{ width: 100, height: 6 }}
                  />
                </Box>
              </ListItem>

              {/* 显示推理路径（如果有） */}
              {data.reasoning_path && data.reasoning_path[index] && (
                <Box sx={{ pl: 4, mb: 2, color: '#666' }}>
                  <Typography variant="caption">
                    推理路径: {data.reasoning_path[index].join(' ')}
                  </Typography>
                </Box>
              )}

              {index < data.relevant_nodes.length - 1 && (
                <Box sx={{ pl: 2, color: '#1976d2' }}>
                  <ArrowRight fontSize="small" />
                </Box>
              )}
            </React.Fragment>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default JointLKEnhancement;
ata, isLoading }) => {
  if (isLoading) {
    return (
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            知识图谱增强推理中...
          </Typography>
          <LinearProgress />
        </CardContent>
      </Card>
    );
  }

  if (!data || !data.relevant_nodes || data.relevant_nodes.length === 0) {
    return null;
  }

  return (
    <Card sx={{ mb: 3, borderLeft: '4px solid #1976d2' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          <Info color="primary" sx={{ verticalAlign: 'middle', mr: 1 }} />
          知识图谱增强推理
        </Typography>

        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          与当前问题最相关的知识节点（由JointLK模型计算）：
        </Typography>

        <List dense>
          {data.relevant_nodes.map(([nodeId, nodeName], index) => (
            <React.Fragment key={nodeId}>
              <ListItem alignItems="center">
                <ListItemText
                  primary={nodeName}
                  secondary={`节点ID: ${nodeId}`}
                />
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Typography variant="body2" sx={{ mr: 1 }}>
                    {Math.round(data.confidence_scores[index] * 100)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={data.confidence_scores[index] * 100}
                    sx={{ width: 100, height: 6 }}
                  />
                </Box>
              </ListItem>

              {/* 显示推理路径（如果有） */}
              {data.reasoning_path && data.reasoning_path[index] && (
                <Box sx={{ pl: 4, mb: 2, color: '#666' }}>
                  <Typography variant="caption">
                    推理路径: {data.reasoning_path[index].join(' ')}
                  </Typography>
                </Box>
              )}

              {index < data.relevant_nodes.length - 1 && (
                <Box sx={{ pl: 2, color: '#1976d2' }}>
                  <ArrowRight fontSize="small" />
                </Box>
              )}
            </React.Fragment>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default JointLKEnhancement;
