import React, { useState } from 'react';
import './search.css';
import { Input, InputGroup, InputLeftElement } from '@chakra-ui/react';
import { PhoneIcon, SearchIcon } from '@chakra-ui/icons';

function Autocomplete() {
    const [inputValue, setInputValue] = useState<string>('');
    const [suggestions, setSuggestions] = useState<string[]>([]);

    const handleInputChange = (event: { target: { value: any; }; }) => {
        const value = event.target.value;
        setInputValue(value);
        if (value.length > 0) {
            const filteredSuggestions = ["Jaipur", "Kota"].filter((suggestion: string) =>
                suggestion.toLowerCase().includes(value.toLowerCase())
            );
            setSuggestions(filteredSuggestions);
        } else {
            setSuggestions([]);
        }
    };

    const handleSuggestionClick = (value: string) => {
        setInputValue(value);
        setSuggestions([]);
    };

    // Event handlers and other methods will go here

    return (
        <>
            <InputGroup>
                <InputLeftElement pointerEvents='none'>
                    <SearchIcon color='gray.300' />
                </InputLeftElement>
                <Input type='tel' placeholder='' />
            </InputGroup>
        </>
        // <div className="autocomplete-wrapper">
        //     <input
        //         type="text"
        //         value={inputValue}
        //         onChange={handleInputChange}
        //         aria-autocomplete="list"
        //         aria-controls="autocomplete-list"
        //     // Additional props
        //     />
        //     {suggestions.length > 0 && (
        //         <ul id="autocomplete-list" className="suggestions-list" role="listbox">
        //             {suggestions.map((suggestion, index) => (
        //                 <li
        //                     key={index}
        //                     onClick={() => handleSuggestionClick(suggestion)}
        //                     role="option"
        //                 // Additional props
        //                 >
        //                     {suggestion}
        //                 </li>
        //             ))}
        //         </ul>
        //     )}
        // </div>
    );
}

export default Autocomplete;