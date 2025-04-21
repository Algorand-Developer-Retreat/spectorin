// examples/rust_example.rs
// Example Solana program
use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint,
    entrypoint::ProgramResult,
    pubkey::Pubkey,
    program_error::ProgramError,
};

entrypoint!(process_instruction);

// Vulnerability: No validation of accounts
pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    
    let source = next_account_info(accounts_iter)?;
    let destination = next_account_info(accounts_iter)?;
    
    // Vulnerability: No check if source is signer
    
    // Vulnerability: No validation of instruction_data
    let amount = instruction_data[0] as u64;
    
    // Vulnerability: No error handling for arithmetic operations
    **source.try_borrow_mut_lamports()? -= amount;
    **destination.try_borrow_mut_lamports()? += amount;
    
    Ok(())
} 