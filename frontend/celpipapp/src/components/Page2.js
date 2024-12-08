import React, { useState } from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";

// Styled components
const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  font-family: "Cinzel", serif;
  font-weight: bold;
  color: inherit;
  margin-bottom: 20px;
  text-align: center;
`;

const Subtitle = styled.h2`
  font-size: 2rem;
  font-family: "Lavishly Yours", cursive;
  font-weight: bold;
  color: inherit;
  margin-bottom: 40px;
  text-align: center;
`;

const FormWrapper = styled.div`
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
`;

const Input = styled.input`
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 200px;
`;

const Dropdown = styled.select`
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 160px;
`;

const Button = styled.button`
  padding: 10px 20px;
  font-size: 1rem;
  font-family: Segoe UI;
  border: none;
  border-radius: 5px;
  background-color: #6200ea;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #3700b3;
  }
`;

const QuizSection = styled.div`
  margin-top: 50px;
  text-align: center;
`;

const QuizButton = styled.button`
  padding: 10px 20px;
  font-size: 1rem;
  font-family: Segoe UI;
  border: none;
  border-radius: 5px;
  background-color: #ff5722;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #e64a19;
  }
`;

const CatchySentence = styled.p`
  font-size: 1rem;
  font-family: "Permanent Marker", cursive;
  color: inherit;
  margin-bottom: 20px;
`;

const ResultWrapper = styled.div`
  margin-top: 20px;
  font-family: Permanent Marker;
  font-size: 1.2rem;
  color: ${(props) => (props.success ? "green" : "red")};
  font-weight: bold;
`;

const Page2 = () => {
  const [wordInput, setWordInput] = useState("");
  const [answerInput, setAnswerInput] = useState("");
  const [quizType, setQuizType] = useState("synonym");
  const [validationMessage, setValidationMessage] = useState("");
  const [isCorrect, setIsCorrect] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();

  const handleQuizRedirect = () => {
    navigate("/");
  };

  const handleWordInputChange = (e) => {
    setWordInput(e.target.value);
  };

  const handleAnswerInputChange = (e) => {
    setAnswerInput(e.target.value);
  };

  const handleQuizTypeChange = (e) => {
    setQuizType(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!wordInput || !answerInput) {
      setValidationMessage("Please enter both the word and answer.");
      return;
    }

    setLoading(true);
    setValidationMessage("");
    
    const requestData = {
      word: wordInput,
      answer: answerInput,
      type: quizType, // either 'synonym' or 'antonym'
    };

    try {
      const response = await fetch("http://localhost:5000/api/validate_quiz", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      const data = await response.json();

      if (response.ok) {
        setIsCorrect(true);
        setValidationMessage(data.message || "Correct answer!");
      } else {
        setIsCorrect(false);
        setValidationMessage(data.message || "Incorrect answer. Try again!");
      }
    } catch (error) {
      setIsCorrect(false);
      setValidationMessage("Error occurred while validating. Please try again.");
    }

    setLoading(false);
  };

  return (
    <Container>
      <Title>Word Quiz</Title>
      <Subtitle>Test your vocabulary knowledge!</Subtitle>
      <FormWrapper>
        <Input
          type="text"
          value={wordInput}
          onChange={handleWordInputChange}
          placeholder="Enter a quiz word"
        />
        <Dropdown value={quizType} onChange={handleQuizTypeChange}>
          <option value="synonym">Synonym</option>
          <option value="antonym">Antonym</option>
        </Dropdown>
        <Input
          type="text"
          value={answerInput}
          onChange={handleAnswerInputChange}
          placeholder="Enter your answer"
        />
      </FormWrapper>
      <Button onClick={handleSubmit} disabled={loading}>
        {loading ? "Checking..." : "Submit"}
      </Button>
      {validationMessage && (
        <ResultWrapper success={isCorrect}>
          {validationMessage}
        </ResultWrapper>
      )}
      <QuizSection>
        <CatchySentence>
          Need more practice?
        </CatchySentence>
        <QuizButton onClick={handleQuizRedirect}>Learn words</QuizButton>
      </QuizSection>
    </Container>
  );
};

export default Page2;
