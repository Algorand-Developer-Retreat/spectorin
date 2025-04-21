// Vulnerable Solana program
use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint,
    entrypoint::ProgramResult,
    pubkey::Pubkey,
    program_error::ProgramError,
};

entrypoint!(process_instruction);

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    
    // Get the account to withdraw from
    let source = next_account_info(accounts_iter)?;
    
    // Get the destination account
    let destination = next_account_info(accounts_iter)?;
    
    // Vulnerability: No check if source is signer
    // Should have: if !source.is_signer { return Err(ProgramError::MissingRequiredSignature); }
    
    // Vulnerability: Using unsafe code
    unsafe {
        // Unsafe code in smart contracts is risky
        let amount = instruction_data.get_unchecked(0) as u64;
        
        // Vulnerability: No arithmetic checks
        // Should use checked_sub and checked_add
        **source.try_borrow_mut_lamports()? -= amount;
        **destination.try_borrow_mut_lamports()? += amount;
    }
    
    Ok(())
} 